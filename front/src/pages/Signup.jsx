import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginPage.css";

const SignupPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault(); // 폼 제출 시 페이지 새로고침 방지
    if (!email || !password) {
      alert("이메일과 비밀번호를 모두 입력해주세요.");
      return;
    }

    setIsLoading(true);

    try {
      // 💡 백엔드 회원가입 API 엔드포인트(/auth/signup)로 주소를 변경합니다.
      const response = await fetch("http://localhost:8000/auth/signup", {
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
        // 백엔드에서 보낸 상세 에러 메시지가 있다면 출력합니다.
        throw new Error(data.detail || "회원가입에 실패했습니다. 입력 정보를 확인하세요.");
      }

      // 💡 백엔드에서 가입 즉시 TokenResponse를 반환하므로 바로 토큰을 저장합니다.
      if (data.access_token) {
        localStorage.setItem("accessToken", data.access_token);
        if (data.refresh_token) {
          localStorage.setItem("refreshToken", data.refresh_token);
        }

        alert("회원가입 및 로그인 성공!");
        navigate("/main"); // 가입 성공 후 바로 메인 페이지로 이동
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
        <h1 className="main_text">Signup</h1>
        
        <form onSubmit={handleSignup}>
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
            <p className="sub_text">
              {isLoading ? "LOADING..." : "START >"}
            </p>
          </button>
        </form>

        <p className="sub_text" style={{ marginTop: "20px", fontSize: "14px" }}>
          이미 계정이 있으신가요?{" "}
          <span 
            className="signup_link" 
            onClick={() => navigate("/login")}
          >
            로그인
          </span>
        </p>

      </div>
    </div>
  );
};

export default SignupPage;