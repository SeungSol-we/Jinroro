const BASE_URL = "http://localhost:8000";

/**
 * 백엔드 API 요청을 보낼 때 인증 토큰을 자동으로 실어주는 공통 함수
 */
export const requestApi = async (endpoint, options = {}) => {
  const accessToken = localStorage.getItem("accessToken");

  // 기본 헤더 설정
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // 토큰이 존재하면 Authorization 헤더에 Bearer 토큰 주입 (백엔드 HTTPBearer 대응)
  if (accessToken) {
    headers["Authorization"] = `Bearer ${accessToken}`;
  }

  const config = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, config);
    
    // 401 Unauthorized 에러가 나면 토큰 만료 가능성 있음 -> 로그인창으로 튕구거나 재발급 필요
    if (response.status === 401) {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      window.location.href = "/"; // 로그인 페이지로 리다이렉트
      throw new Error("인증이 만료되었습니다. 다시 로그인해주세요.");
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "요청 처리 중 오류가 발생했습니다.");
    }

    return data;
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
};