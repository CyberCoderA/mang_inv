import React, { useState, useEffect } from "react";
import axios from "axios";
import Logo from "../assets/logo.png";
import { Link } from "react-router-dom";

const SignUp = () => {
    const [userType, setUserType] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [fullname, setFullname] = useState("");
    const [userRoles, setUserRoles] = useState([]);

    // fetch roles once on mount
    useEffect(() => {
        let cancelled = false;
        axios.get('/api/user_roles/getAllRoles')
            .then(response => {
                const data = response.data || {};
                if (data.error) {
                    alert(`Error: ${data.error}`);
                    return;
                }
                if (!cancelled) setUserRoles(data.roles || []);
            })
            .catch(error => {
                console.error("There was an error retrieving user roles!", error);
                alert("Failed to retrieve user roles.");
            });

        return () => { cancelled = true };
    }, []);

    function renderUserRoles() {
        return userRoles.map((role) => (
            <option key={role.user_role_id} value={role.user_role_id}>{role.user_role_title}</option>
        ));
    }
    

    // handle sign up
    function handleSignUp() {
        axios.post('/api/users/signup', {
            user_type: userType,
            username: username,
            password: password,
            full_name: fullname,
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
            console.error("There was an error signing up!", error);
            alert("Sign up failed.");
        });
    }

    return (
        <div className="bg-blue-900 h-screen w-screen flex flex-col justify-center items-center">
            <div className="h-[60%] max-h-[1000px] w-11/12 max-w-96 flex flex-col items-center justify-around bg-white backdrop-blur-xl rounded-xl px-6 lg:max-w-[900px] min-h-[400px] shadow-2xl">
                {/* Logo */}
                <div className="flex flex-row items-center gap-2 lg:gap-5">
                    <img src={Logo} alt="logo" className="h-6 lg:h-15" />
                    <h1 className="text-sm font-bold text-gray-900 lg:text-4xl">Inventory Management System</h1>
                </div>

                <div className="w-full h-[72%] flex flex-col items-center gap-2 p-4">
                    <h1 className="text-2xl font-bold text-gray-900 lg:text-4xl">SIGN UP</h1>
                    <div className="h-full w-full flex flex-col gap-5 overflow-y-auto">
                        <div className="flex flex-col gap-2">
                            <label htmlFor="user-roles" className="text-3xl font-bold">User Type: </label>
                            <select className="h-12 p-2 border-2 border-black rounded-xl" name="user-roles" id="user-roles" value={userType} onChange={(e) => setUserType(e.target.value)}>
                                <optgroup>
                                    {renderUserRoles()}
                                </optgroup>
                            </select>
                        </div>

                        <div className="flex flex-col gap-2">
                            <label htmlFor="fullname-field" className="text-3xl font-bold">Full Name</label>
                            <input id="fullname-field" type="text" className="h-12 w-full border-2 p-2 text-xl rounded-lg" value={fullname} onChange={(e) => setFullname(e.target.value)} />
                        </div>

                        <div className="flex flex-col gap-2">
                            <label htmlFor="username-field" className="text-3xl font-bold">Username</label>
                            <input id="username-field" type="text" className="h-12 w-full border-2 p-2 text-xl rounded-lg" value={username} onChange={(e) => setUsername(e.target.value)} />
                        </div>

                        <div className="flex flex-col gap-2">
                            <label htmlFor="password-field" className="text-3xl font-bold">Password</label>
                            <input id="password-field" type="password" className="h-12 w-full border-2 p-2 text-xl rounded-lg" value={password} onChange={(e) => setPassword(e.target.value)} />
                        </div>
                        
                        <button className="w-full h-[20%] p-3 rounded-xl bg-blue-900 text-white text-2xl hover:cursor-pointer hover:text-3xl hover:font-bold" onClick={() => handleSignUp()}>SIGN UP</button>
                    </div>
                </div>

                <h1 className="text-xl">Already have an account? <Link to={"/login"} className="justify-self-end text-xl font-bold text-indigo-600">Login!</Link></h1>
            </div>
        </div>
    );
};

export default SignUp;