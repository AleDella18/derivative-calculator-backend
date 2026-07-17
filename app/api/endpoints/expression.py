from fastapi import APIRouter, HTTPException, Request
from jose import JWTError
from app.schemas.expression import ExpressionRequest, ExpressionResponse
from app.utils.utils import jwt_decoder
from app.services.compute_derivative import compute_derivative
from app.services.graphic_generator import graphic_generator
from app.repository.expressions import (
    get_existing_derivative,
    get_image_path,
    save_derivative,
    get_function_id,
    save_graphic,
)
import logging
import os


router = APIRouter(tags=["expression"])

SECRET_KEY = os.getenv("SECRET_KEY", "BrUJTuTS28idUj5sfo2370BkUREjY3M2CJjp01UVrNm")
ALGORITHM = "HS256"

logger = logging.getLogger(__name__)


@router.post("/expression", response_model=ExpressionResponse)
def compute_expression(req: ExpressionRequest, request: Request):
    try:
        token = request.headers.get("cookie")

        if not token:
            logger.warning("Missing authentication token")
            raise HTTPException(status_code=401, detail="Authentication required")

        token = token.replace("auth_token=", "")

        username = jwt_decoder(token)
        if not username:
            logger.warning("Invalid authentication token")
            raise HTTPException(status_code=401, detail="Invalid token")

        db = request.app.state.db
        derivative = get_existing_derivative(req.expr, db)

        if derivative:
            function_id = get_function_id(req.expr, db)
            image_path = get_image_path(function_id, db)
            return {"derivative": derivative, "img_path": image_path}

        condition, derivative = compute_derivative(req.expr, req.diff_var)

        if not condition:
            logger.warning(
                "Invalid expression | expr=%s | reason=%s", req.expr, derivative
            )
            raise HTTPException(status_code=400, detail=derivative)

        save_derivative(username, req.expr, derivative, db)
        function_id = get_function_id(req.expr, db)
        image_path = graphic_generator(derivative, req.diff_var, function_id)
        save_graphic(function_id, image_path, db)

        return {"derivative": derivative, "img_path": image_path}

    except JWTError:
        logger.warning("Expired or malformed token")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    except HTTPException:
        raise

    except Exception as e:
        logger.error("Unexpected error while processing '%s': %s", req.expr, str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


