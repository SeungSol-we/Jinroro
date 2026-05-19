import "./MainPage.css"
import { useNavigate } from 'react-router-dom';
import Header from "../component/Header";

const MainPage = () => {
    const navigation = useNavigate();

    return(
        <div className="wrap">
            <Header />
            <div className='text_wrap'>
                <h1 className='main_text'>진로로</h1>
                
            </div>
        </div>
    );
}

export default MainPage;