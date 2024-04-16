const api = (token) => {
  const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

  const headers = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = "Bearer " + token;
  }

  const get = (url) =>
    fetch(baseUrl + url, { method: "GET", headers, mode: "no-cors" });

  const post = (url, body) =>
    fetch(baseUrl + url, {
      method: "POST",
      body: JSON.stringify(body),
      headers,
      mode: "no-cors",
    });

  const postForm = (url, body) =>
    fetch(baseUrl + url, {
      method: "POST",
      body: new URLSearchParams(body),
      headers: {
        ...headers,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      mode: "no-cors",
    });

  return { get, post, postForm };
};

export default api;
