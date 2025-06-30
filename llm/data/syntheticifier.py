import json
import random
import uuid
from datetime import datetime, timedelta, timezone
import os
import base64

# --- Persona-Driven Data Structures for Contextual Realism ---

# Define server "personas" to ensure logical consistency.
# Each persona dictates which domains, server headers, paths, and logic to use.
SERVER_PERSONAS = [
    {
        "name": "CLOUDFLARE_API",
        "server_type": "CLOUDFLARE_NGINX_GUNICORN",
        "description": "A Python API server running on Gunicorn, behind an Nginx reverse proxy and Cloudflare.",
        "server_headers": ["nginx/1.25.3", "cloudflare"],
        "app_server_headers": ["gunicorn/21.2.0", "Werkzeug/3.0.1 Python/3.11.4"],
        "domains": [
            "api.example.com",
            "auth.mycompany.dev",
            "backend.app-service.xyz",
            "events.logstream.io",
            "staging-api.internal-tool.com",
        ],
        "paths": {
            "common": [
                "/api/v1/users",
                "/api/v2/organizations/{org_id}/members",
                "/oauth/token",
                "/health",
            ],
            "rare": ["/api/v1/posts/{post_id}/comments", "/metrics/daily"],
        },
        "cookie_logic": ["generic", "cloudflare"],
        "header_logic": ["cloudflare"],
        "response_logic": "generic_api",
    },
    {
        "name": "PORTAINER_INSTANCE",
        "server_type": "PORTAINER_GO",
        "description": "A self-hosted Portainer instance using its internal Go web server.",
        "server_headers": [],
        "domains": ["po.smp46.me", "portainer.internal-tool.com"],
        "paths": {
            "common": ["/api/settings", "/api/users/me", "/api/settings/public"],
            "rare": ["/api/users/{user_id}", "/api/endpoints"],
        },
        "cookie_logic": ["portainer", "gorilla_csrf"],
        "header_logic": [],
        "response_logic": "portainer_specific",
    },
    {
        "name": "AWS_S3_ASSETS",
        "server_type": "AWS_S3",
        "description": "Direct hosting of assets from an Amazon S3 bucket.",
        "server_headers": ["AmazonS3"],
        "domains": [
            "customer-uploads.s3.amazonaws.com",
            "cdn.myassets.com",
            "assets.marketing-site.co",
        ],
        "paths": {
            "common": [
                "/images/{uuid}.jpg",
                "/downloads/invoice-{date}.pdf",
                "/assets/css/main.{hash}.css",
            ],
            "rare": ["/video-previews/{id}/thumbnail.png", "/favicon.ico"],
        },
        "cookie_logic": [],
        "header_logic": ["s3"],
        "response_logic": "file_or_error",
    },
    {
        "name": "GRAPHQL_API",
        "server_type": "CLOUDFLARE_APOLLO_NODE",
        "description": "A Node.js GraphQL API using Apollo Server, fronted by Cloudflare.",
        "server_headers": ["cloudflare"],
        "app_server_headers": ["Cowboy"],
        "domains": ["graphql.new-platform.dev", "gql.service.org"],
        "paths": {"common": ["/graphql"], "rare": ["/v1/graphql", "/playground"]},
        "cookie_logic": ["generic", "cloudflare"],
        "header_logic": ["cloudflare"],
        "response_logic": "graphql_api",
    },
    {
        "name": "INTERNAL_RPC",
        "server_type": "INTERNAL_GO",
        "description": "An internal RPC service, likely using Go.",
        "server_headers": ["Go-http-client/2.0"],
        "domains": ["rpc.internal-comm.local", "twirp.service.internal"],
        "paths": {
            "common": [
                "/twirp/com.example.Haberdasher/MakeHat",
                "/rpc/Users/GetProfile",
            ],
            "rare": [],
        },
        "cookie_logic": [],
        "header_logic": [],
        "response_logic": "generic_api",
    },
    {
        "name": "VERCEL_FRONTEND",
        "server_type": "VERCEL",
        "description": "A modern web frontend hosted on Vercel.",
        "server_headers": ["Vercel"],
        "domains": ["www.ecommerce.com", "blog.techinsights.net", "status.main-app.io"],
        "paths": {
            "common": [
                "/home",
                "/products/{product_id}",
                "/_next/data/{build_id}/index.json",
            ],
            "rare": ["/about-us", "/api/revalidate"],
        },
        "cookie_logic": ["generic"],
        "header_logic": ["vercel"],
        "response_logic": "html_or_json",
    },
]

# --- Shared Data Pools (Used by Personas) ---

methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"]
status_codes = [
    200,
    201,
    204,
    301,
    302,
    304,
    400,
    401,
    403,
    404,
    409,
    429,
    500,
    502,
    503,
]
STATUS_TEXTS = {
    200: "OK",
    201: "Created",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    304: "Not Modified",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    409: "Conflict",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
}
request_user_agents = [
    # Desktop
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.10 Safari/605.1.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3",
    "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
    # Mobile
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.3",
    # Programmatic
    "PostmanRuntime/7.35.0",
    "curl/8.4.0",
    "Python/3.11 aiohttp/3.9.1",
]
server_user_agents = [
    "Python-urllib/3.11",
    "Go-http-client/2.0",
    "Apache-HttpClient/5.2.1 (Java/17.0.7)",
    "GitHub-Hookshot/f3a0d9b",
    "Stripe/1.0 (+https://support.stripe.com/questions/what-is-the-user-agent-for-stripe-webhooks)",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.1; +https://openai.com/gptbot)",
]
content_types = [
    "application/json",
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain",
    "text/html",
]

# --- Contextual Generation Functions (largely unchanged) ---


def generate_csrf_token():
    return base64.b64encode(os.urandom(48)).decode("utf-8").replace("=", "")


def generate_mock_jwt():
    header = (
        base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').decode().rstrip("=")
    )
    payload_data = {
        "sub": str(uuid.uuid4()),
        "exp": int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
        "iat": int(datetime.now(timezone.utc).timestamp()),
    }
    payload = (
        base64.urlsafe_b64encode(json.dumps(payload_data).encode()).decode().rstrip("=")
    )
    signature = base64.urlsafe_b64encode(os.urandom(32)).decode().rstrip("=")
    return f"{header}.{payload}.{signature}"


def generate_cookie_header(persona):
    cookies = []
    cookie_logic = persona.get("cookie_logic", [])
    if "cloudflare" in cookie_logic and random.random() < 0.7:
        cookies.append(
            f"cf_clearance={str(uuid.uuid4()).replace('-', '')}-{int(datetime.now(timezone.utc).timestamp())}-1.2.1.1"
        )
        if random.random() < 0.5:
            cookies.append(f"CF_Authorization={generate_mock_jwt()}")
    if "portainer" in cookie_logic:
        cookies.append(f"portainer_api_key={generate_mock_jwt()}")
    if "gorilla_csrf" in cookie_logic and random.random() < 0.8:
        gorilla_csrf_val = f"{int(datetime.now(timezone.utc).timestamp())}|{base64.b64encode(os.urandom(30)).decode()}"
        cookies.append(f"_gorilla_csrf={gorilla_csrf_val}")
    if "generic" in cookie_logic and random.random() < 0.4:
        cookies.append(f"session_id={str(uuid.uuid4())}")
    return "; ".join(cookies) if cookies else None


def generate_request_body(method, path, content_type):
    if method in ["GET", "HEAD", "OPTIONS", "DELETE"]:
        return None
    if "/graphql" in path and content_type == "application/json":
        query = random.choice(
            [
                'query { user(id: "1") { id name email } }',
                'mutation { createUser(input: { name: "Test", email: "test@example.com" }) { id } }',
            ]
        )
        return json.dumps({"query": query})
    if content_type == "application/json":
        return json.dumps(
            {
                "action": "update",
                "item_id": str(uuid.uuid4()),
                "data": {"status": "active", "value": random.randint(1, 100)},
            }
        )
    elif content_type == "application/x-www-form-urlencoded":
        return f"username=testuser&password={str(uuid.uuid4())[:12]}&_csrf={generate_csrf_token()[:16]}"
    elif content_type == "text/plain":
        return "Log entry: User logged in successfully."
    else:
        return None


def generate_response_body(persona, path, status_code, content_type):
    response_logic = persona.get("response_logic")
    if not (200 <= status_code < 300):
        if content_type == "application/json":
            return json.dumps(
                {
                    "error": STATUS_TEXTS.get(status_code, "Error"),
                    "message": f"An error occurred while processing the request for {path}",
                    "request_id": str(uuid.uuid4()),
                }
            )
        elif content_type == "text/html":
            return f"<html><body><h1>{status_code} {STATUS_TEXTS.get(status_code, 'Error')}</h1></body></html>"
        return STATUS_TEXTS.get(status_code, "Error")
    if response_logic == "portainer_specific":
        return generate_portainer_specific_body(path, status_code)
    if response_logic == "graphql_api" and content_type == "application/json":
        return json.dumps(
            {
                "data": {
                    "user": {"id": "1", "name": "smp46", "email": "smp46@example.com"}
                }
            }
        )
    if response_logic == "file_or_error" or content_type not in [
        "application/json",
        "text/html",
    ]:
        return None
    if response_logic == "html_or_json":
        if content_type == "text/html":
            return "<html><body><h1>Welcome</h1><p>Page loaded successfully.</p></body></html>"
    return json.dumps(
        {"success": True, "data": {"id": str(uuid.uuid4()), "status": "processed"}}
    )


def generate_portainer_specific_body(path, status_code):
    if "/api/settings/public" in path:
        return json.dumps(
            {"AuthenticationMethod": 1, "EnableTelemetry": False, "LogoURL": ""}
        )
    if "/api/users/me" in path:
        return json.dumps({"Id": 1, "Username": "smp46", "Role": 1})
    if "/api/settings" in path:
        return json.dumps(
            {"AuthenticationMethod": 1, "LDAPSettings": {"AnonymousMode": True}}
        )
    return generate_response_body({}, path, status_code, "application/json")


def generate_contextual_headers(persona, now, request_headers):
    headers = {"date": now.strftime("%a, %d %b %Y %H:%M:%S GMT")}
    header_logic = persona.get("header_logic", [])
    if "cloudflare" in header_logic:
        headers["cf-cache-status"] = random.choice(
            ["DYNAMIC", "HIT", "MISS", "EXPIRED"]
        )
        headers["cf-ray"] = (
            f"{uuid.uuid4().hex[:16]}-{random.choice(['SYD', 'LAX', 'LHR'])}"
        )
        headers["server"] = "cloudflare"
        if random.random() < 0.5:
            headers["expect-ct"] = (
                'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"'
            )
    if "vercel" in header_logic:
        headers["x-vercel-id"] = (
            f"{random.choice(['syd1', 'sfo1'])}::{uuid.uuid4().hex[:5]}-{int(now.timestamp())}"
        )
        headers["x-vercel-cache"] = random.choice(["HIT", "MISS", "STALE"])
        headers["server"] = "Vercel"
    if "s3" in header_logic:
        headers["x-amz-id-2"] = base64.b64encode(os.urandom(64)).decode()
        headers["x-amz-request-id"] = uuid.uuid4().hex.upper()[:16]
        headers["accept-ranges"] = "bytes"
        headers["server"] = "AmazonS3"
    if "server" not in headers:
        server_pool = persona.get("server_headers", []) + persona.get(
            "app_server_headers", []
        )
        if server_pool:
            headers["server"] = random.choice(server_pool)
    headers["x-content-type-options"] = "nosniff"
    headers["x-frame-options"] = "SAMEORIGIN"
    headers["vary"] = (
        "Accept-Encoding, Cookie" if "cookie" in request_headers else "Accept-Encoding"
    )
    return headers


def generate_http_sample(force_method=None):
    """
    Generates a single, contextually coherent HTTP request/response sample.
    Can be forced to generate a sample for a specific HTTP method.
    """
    # 1. Choose a Persona to drive all other choices
    if force_method == "GET":
        # Filter personas to those that are suitable for GET requests
        suitable_personas = [
            p
            for p in SERVER_PERSONAS
            if p["name"] not in ["INTERNAL_RPC", "GRAPHQL_API"]
        ]
        persona = random.choice(suitable_personas)
    else:
        persona = random.choice(SERVER_PERSONAS)

    # 2. Select Method and Path based on Persona
    if force_method:
        method = force_method
    else:
        method = random.choice(methods)

    path_pool = persona["paths"]["common"] + persona["paths"]["rare"]
    if not path_pool:
        path_template = "/"
    else:
        path_template = random.choice(path_pool)

    # For forced GETs, avoid paths that only make sense with other methods
    if force_method == "GET" and any(
        p in path_template
        for p in ["/oauth/token", "/api/revalidate", "/twirp/", "/rpc/"]
    ):
        path_template = "/health"  # Default to a safe GET path

    path = path_template.format(
        org_id=f"org_{uuid.uuid4().hex[:12]}",
        post_id=random.randint(100, 9999),
        user_id=random.randint(1, 100),
        uuid=uuid.uuid4(),
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        hash=uuid.uuid4().hex[:8],
        build_id=uuid.uuid4().hex,
        product_id=random.randint(1000, 9999),
        id=random.randint(1, 99999),
    )

    # Override method for certain paths for realism, unless method is forced
    if not force_method:
        if "graphql" in path:
            method = "POST"
        if any(x in path for x in [".jpg", ".css", ".pdf", ".png"]):
            method = "GET"
        if path == "/api/revalidate":
            method = "POST"

    domain = random.choice(persona["domains"])
    url = f"https://{domain}{path}"
    now = datetime.now(timezone.utc)

    # 3. Generate Request based on Persona and context
    is_server_request = "rpc" in persona["name"].lower() or random.random() < 0.1
    user_agent = random.choice(
        server_user_agents if is_server_request else request_user_agents
    )
    request_content_type = (
        "application/json"
        if "api" in path or "graphql" in path
        else random.choice(content_types)
    )
    request_body = generate_request_body(method, path, request_content_type)
    cookie_header = generate_cookie_header(persona)
    request_headers = {
        "user-agent": user_agent,
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "connection": "keep-alive",
    }
    if cookie_header:
        request_headers["cookie"] = cookie_header
    if method in ["POST", "PUT", "PATCH"] and request_body:
        request_headers["origin"] = f"https://{domain}"
        request_headers["content-type"] = request_content_type
        request_headers["content-length"] = str(len(request_body.encode()))
        if "portainer" in persona["cookie_logic"]:
            request_headers["x-csrf-token"] = generate_csrf_token()

    req_lines = [f"{method} {url} HTTP/1.1", f"host: {domain}"] + [
        f"{k}: {v}" for k, v in sorted(request_headers.items())
    ]
    prompt_string = (
        "\n".join(req_lines) + "\n\n" + (request_body if request_body else "")
    )

    # 4. Generate Response based on Persona and Request
    status = random.choice(status_codes)
    rnum = random.random()
    if rnum < 0.8:
        status = 200

    if method == "OPTIONS":
        status = 204
    if method == "POST" and "graphql" not in path and status == 200:
        status = 201
    if method == "GET" and status == 201:
        status = 200  # GET shouldn't return 201

    response_headers = generate_contextual_headers(persona, now, request_headers)
    response_content_type = (
        "application/json"
        if persona.get("response_logic")
        in ["generic_api", "graphql_api", "portainer_specific"]
        else "text/html"
    )
    response_body = generate_response_body(persona, path, status, response_content_type)
    if method == "HEAD" or status == 204:
        response_body = None
    if response_body:
        response_headers["content-type"] = response_content_type
        response_headers["content-length"] = str(len(response_body.encode()))
    else:
        response_headers.pop("content-type", None)

    status_text = STATUS_TEXTS.get(status, "OK")
    res_lines = [f"HTTP/1.1 {status} {status_text}"] + [
        f"{k}: {v}" for k, v in sorted(response_headers.items())
    ]
    response_string = (
        "\n".join(res_lines) + "\n\n" + (response_body if response_body else "")
    )

    return {"prompt": prompt_string.strip(), "response": response_string.strip()}

def main():
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    # --- Configuration for skewed generation ---
    num_samples = 5000
    get_request_skew = 0.70  # 70% of the data will be GET requests

    num_get_samples = int(num_samples * get_request_skew)
    num_other_samples = num_samples - num_get_samples

    all_samples = []

    # --- Generation Phase ---
    print(f"Generating {num_other_samples} mixed-method HTTP samples...")
    for _ in range(num_other_samples):
        all_samples.append(generate_http_sample())

    print(f"Generating {num_get_samples} GET-only HTTP samples to skew the dataset...")
    for _ in range(num_get_samples):
        all_samples.append(generate_http_sample(force_method="GET"))

    # --- Finalization Phase ---
    print("Shuffling all samples for a random distribution...")
    random.shuffle(all_samples)

    output_file_path = os.path.join(output_dir, "synthetic_http_traffic_skewed.jsonl")
    print(f"Writing {num_samples} skewed samples to '{output_file_path}'...")
    with open(output_file_path, "w") as f:
        for sample in all_samples:
            f.write(json.dumps(sample) + "\n")

    print(f"Successfully generated a realistically skewed dataset.")

# --- Main Execution ---
if __name__ == "__main__":
    main()