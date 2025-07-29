def build_auth_header(api_key, email):
    return {"X-Api-Key": api_key, "X-User-Email": email}
