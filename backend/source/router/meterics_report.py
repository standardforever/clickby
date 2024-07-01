
from fastapi import APIRouter, Depends, HTTPException, status, Security, Response
from typing import Annotated, List, Union

from common.models.user_models import User, UserSafe

from utils.auth_utils import get_current_active_user



router = APIRouter(
	tags=["Users Management"]
)

@router.get("/healthz")
async def healthz():
	return {"ok": "ok"}


DATABASE_NAME="mvp2"
WEBSITE_COLLECTION="Website_collection"
SP_UPC_LOOKUP="sp_upc_lookup"
SP_UPC_LOOKUP2="sp_upc_lookup2"
SP_GSL_LOOKUP2="sp_gsl_lookup2"
ASIN_MASTER_UPC="asin_master_upc"


@router.get('/win-asin-uk-amz')
async def win_asin_uk_amz():
	pass

@router.get('/win-asin-us-amz')
async def win_asin_us_amz():
	pass

@router.get('/win-ecom-us-amz')
async def win_ecom_us_amz():
	pass

@router.get('/win-ecom-uk-amz')
async def win_ecom_uk_amz():
	pass

@router.get('/win-ecom-uk-amz')
async def win_ecom_uk_amz():
	pass

@router.get('/total-asin-reivew')
async def total_asin_review():
	pass

@router.get('/total-uk-ecom-product-ai-review-profit')
async def total_uk_ecom_product_ai_review_profit():
	pass

@router.get('/total-uk-ecom-product-ai-review-profit/')
async def total_uk_ecom_product_ai_review_profit():
	pass