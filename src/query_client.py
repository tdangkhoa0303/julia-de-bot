from requests import post, Response

headers = {"Authorization": "Bearer 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"}

def api_post(api_url: str, payload: any) -> Response:
	return post(
    api_url, 
    headers=headers, 
    json=payload
  )
