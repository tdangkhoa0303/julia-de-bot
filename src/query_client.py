from requests import post, Response

from .configs import ENV

headers = {"Authorization": f"Bearer {ENV['HUGGING_FACE_TOKEN']}"}

def api_post(api_url: str, payload: any) -> Response:
	return post(
    api_url, 
    headers=headers, 
    json=payload
  )
