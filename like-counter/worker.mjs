const LIKE_PATH = "/likes";
const VISITOR_ID_PATTERN = /^[A-Za-z0-9_-]{20,80}$/;
const LOCAL_ORIGINS = new Set(["http://localhost:8000", "http://127.0.0.1:8000"]);

function corsHeaders(request, env) {
  const origin = request.headers.get("Origin") || "";
  const allowed = origin === env.ALLOWED_ORIGIN || LOCAL_ORIGINS.has(origin);
  if (!allowed) return null;

  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
  };
}

function json(data, status, cors) {
  return Response.json(data, {
    status,
    headers: {
      ...cors,
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
    },
  });
}

async function readCount(db) {
  const row = await db.prepare("SELECT COUNT(*) AS count FROM website_likes").first();
  return Number(row?.count || 0);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== LIKE_PATH) {
      return new Response("Not found", { status: 404 });
    }

    const cors = corsHeaders(request, env);
    if (request.method === "OPTIONS") {
      return cors
        ? new Response(null, { status: 204, headers: cors })
        : new Response("Origin not allowed", { status: 403 });
    }
    if (!cors) return new Response("Origin not allowed", { status: 403 });

    try {
      if (request.method === "GET") {
        return json({ count: await readCount(env.DB) }, 200, cors);
      }

      if (request.method !== "POST") {
        return json({ error: "Method not allowed" }, 405, cors);
      }

      const body = await request.json();
      const visitorId = typeof body.visitor_id === "string" ? body.visitor_id : "";
      if (!VISITOR_ID_PATTERN.test(visitorId) || typeof body.liked !== "boolean") {
        return json({ error: "Invalid request" }, 400, cors);
      }

      const rateLimitKey = request.headers.get("CF-Connecting-IP") || visitorId;
      const rateLimit = await env.LIKE_RATE_LIMITER.limit({ key: rateLimitKey });
      if (!rateLimit.success) {
        return json({ error: "Please wait before trying again" }, 429, cors);
      }

      if (body.liked) {
        await env.DB.prepare(
          "INSERT OR IGNORE INTO website_likes (visitor_id) VALUES (?)"
        ).bind(visitorId).run();
      } else {
        await env.DB.prepare(
          "DELETE FROM website_likes WHERE visitor_id = ?"
        ).bind(visitorId).run();
      }

      const count = await readCount(env.DB);
      const savedLike = await env.DB.prepare(
        "SELECT 1 AS liked FROM website_likes WHERE visitor_id = ?"
      ).bind(visitorId).first();
      return json({ count, liked: Boolean(savedLike) }, 200, cors);
    } catch (error) {
      console.error("Like counter request failed", error);
      return json({ error: "Counter unavailable" }, 503, cors);
    }
  },
};
