import React, { useContext } from "react"
import routes from "./routes"
import { Link, Redirect } from "react-router-dom"
import { AuthContext } from "./App"
import * as firebase from "firebase"

const Header = () => {

    const logout = () => {
        console.log('Logging out');
        firebase.auth().signOut()
        .then(function() {
            // Sign-out successful.
            
        })
        .catch(function(error) {
            // An error happened
        });
    }

    const { isLoggedIn } = useContext(AuthContext)
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
            {/* <a className="navbar-brand" href="#">
                Navbar
            </a> */}
            <button
                className="navbar-toggler"
                type="button"
                data-toggle="collapse"
                data-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span className="navbar-toggler-icon"></span>
            </button>

            <div
                className="collapse navbar-collapse"
                id="navbarSupportedContent"
            >
                <ul className="navbar-nav mr-auto">
                    {!isLoggedIn && routes.map((route, i) => (
                        <li className="nav-item" key={i}>
                            <Link to={route.path} className="nav-link">{route.name}</Link>
                        </li>
                    ))}
                    {isLoggedIn && <>
                        <li className="nav-item">
                            <Link to="/reports" className="nav-link">Reports</Link>
                        </li>
                        <li className="nav-item" onClick={logout}>
                            <span className="nav-link">Log out</span>
                        </li>
                    </>}
                    <li className="nav-item">
                        <span className="nav-link disabled" tabIndex="-1" aria-disabled="true">Logged in: {JSON.stringify(isLoggedIn)}</span>
                    </li>
                </ul>
            </div>
        </nav>
    )
}

export default Header
