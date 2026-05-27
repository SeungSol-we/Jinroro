import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginPage.css";

const LoginPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault(); // 폼 제출 시 페이지 새로고침 방지
    if (!email || !password) {
      alert("이메일과 비밀번호를 모두 입력해주세요.");
      return;
    }

    setIsLoading(true);

    try {
      // 💡 백엔드가 /auth/login 엔드포인트를 사용하므로 주소를 맞춰줍니다.
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        // 백엔드에서 에러 메시지를 보냈다면 해당 메시지 출력, 없다면 기본 메시지
        throw new Error(data.detail || "로그인에 실패했습니다. 계정을 확인하세요.");
      }

      // 💡 백엔드 TokenResponse 명세에 맞게 토큰을 저장합니다.
      if (data.access_token) {
        localStorage.setItem("accessToken", data.access_token);
        if (data.refresh_token) {
          localStorage.setItem("refreshToken", data.refresh_token);
        }

        alert("로그인 성공!");
        navigate("/main"); // 로그인 성공 후 메인 페이지로 이동
      } else {
        throw new Error("토큰 정보가 올바르지 않습니다.");
      }
    } catch (error) {
      alert(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="wrap">
      <div className="text_wrap">
        <h1 className="main_text">Login</h1>
        
        <form onSubmit={handleLogin}>
          <div className="input_group">
            <input
              type="email"
              placeholder="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isLoading}
              required
            />
            <input
              type="password"
              placeholder="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
              required
            />
          </div>
          
          <button type="submit" className="go" disabled={isLoading}>
              <p className="button_text">
                {isLoading ? "LOADING..." : "START"}
              </p>
          </button>
        </form>
        <p className="sub_text">
          아직 계정이 없으신가요?{" "}
          <span className="signup_link" onClick={() => navigate("/signup")}>
            회원가입
          </span>
        </p>

      </div>
    </div>
  );
};

export default LoginPage;