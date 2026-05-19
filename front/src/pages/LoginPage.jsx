import "./LoginPage.css"
import { useNavigate } from 'react-router-dom';


const LoginPage = () => {
    const navigation = useNavigate();

    return(
        <div className="wrap">
            <div className='text_wrap'>
                <h1 className='main_text'>Login</h1>
                <div>
                    <input type="text" placeholder="user id" />
                    <input type="text" placeholder="email" />
                    <input type="text" placeholder="password" />
                </div>
                <button className='go' onClick={() => navigation('#')}>
                    <p className='sub_text'>START &gt;</p>
                </button>
            </div>
        </div>
    );
}

export default LoginPage;