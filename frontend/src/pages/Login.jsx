import React, {useState} from "react";
import axios from "axios";
import Logo from "../assets/logo.png";
import { Link } from "react-router-dom";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    // Handle login
    function handleLogin() {
        axios.post('/api/users/login', {
            username: username,
            password: password
        }).then(response => {
            const data = response.data || {};
            // If backend returns an explicit error
            if (data.error) {
                alert(`Error: ${data.error}`);
                return;
            }

            // Backend returns { exists: true/false }
            if (data.exists === true) {
                alert(`User "${username}" found.`);
            } else if (data.exists === false) {
                alert(`User "${username}" not found.`);
            } else {
                // Fallback: show raw response
                alert(JSON.stringify(data));
            }
        }).catch(error => {
            console.error("There was an error logging in!", error);
            // Extract HTTP status and server message if available
            const status = error?.response?.status;
            const statusText = error?.response?.statusText || '';
            const serverMsg = error?.response?.data?.error || error?.response?.data?.message;
            const fallbackMsg = error.message || 'Unknown error';
            const combinedMsg = serverMsg || fallbackMsg;
            const alertMsg = status
                ? `Login failed (${status} ${statusText}): ${combinedMsg}`
                : `Login request failed: ${combinedMsg}`;
            alert(alertMsg);
        });
    }

    return (
    <div className="bg-blue-900 h-screen w-screen flex flex-col justify-center items-center">
        {/* Modal */}
        <div className="h-[60%] max-h-[1000px] w-11/12 max-w-96 flex flex-col items-center justify-around bg-white backdrop-blur-xl rounded-xl px-6 lg:max-w-[900px] min-h-[400px] shadow-2xl">
            {/* Logo */}
            <div className="flex flex-row items-center gap-2 lg:gap-5">
                <img src={Logo} alt="logo" className="h-6 lg:h-15"/>
                <h1 className="text-sm font-bold text-gray-900 lg:text-4xl">Inventory Management System</h1>
            </div>

            <div className="w-full h-[50%] flex flex-col items-center gap-5 p-4">
                <h1 className="text-2xl font-bold text-gray-900 lg:text-4xl">LOGIN</h1>
                <div className="h-full w-full flex flex-col gap-10">
                    <div className="flex flex-col gap-2">
                        <label htmlFor="username-field" className="text-3xl font-bold">Username</label>
                        <input id="username-field" type="text" className="h-12 w-full border-2 p-2 text-xl rounded-lg" value={username} onChange={(e) => setUsername(e.target.value)}/>
                    </div>
                    <div className="flex flex-col gap-2">
                        <label htmlFor="password-field" className="text-3xl font-bold">Password</label>
                        <input id="password-field" type="password" className="h-12 w-full border-2 p-2 text-xl rounded-lg" value={password} onChange={(e) => setPassword(e.target.value)}/>
                        <Link to={"#"}><h1 className="justify-self-end text-xl font-bold text-indigo-600">Forgot password?</h1></Link>
                    </div>
                    <button className="w-full h-100 p-3 rounded-xl bg-blue-900 text-white text-2xl hover:cursor-pointer hover:text-3xl hover:font-bold" onClick={() => handleLogin()}>LOGIN</button>
                </div>
            </div>

            <h1 className="text-xl">Don't have an account? <Link to={"/signup"} className="justify-self-end text-xl font-bold text-indigo-600">Sign Up!</Link></h1>
        </div>
    </div>
    );
};

export default Login;