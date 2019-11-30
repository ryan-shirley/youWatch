import React, { useState, useEffect } from "react"
import ReactDOM from "react-dom"
import { Switch, BrowserRouter as Router, Route } from "react-router-dom"
import routes from "./routes.js"
import Header from "./Header"
import "./styles.css"
import "./App.scss"

import protectedRoutes from "./protectedRoutes"
import * as firebase from "firebase"
import firebaseConfig from "./firebase.config"

import ProtectedRouteHoc from "./ProtectedRouteHoc"

firebase.initializeApp(firebaseConfig)

export const AuthContext = React.createContext(null)

function App() {
    const [isLoggedIn, setLoggedIn] = useState(false)

    function readSession() {
        const user = window.sessionStorage.getItem(
            `firebase:authUser:${firebaseConfig.apiKey}:[DEFAULT]`
        )
        if (user) setLoggedIn(true)
    }
    useEffect(() => {
        readSession()
    }, [])

    return (
        <AuthContext.Provider value={{ isLoggedIn, setLoggedIn }}>
            <div className="App">
                <Router>
                    <Header isLoggedIn={isLoggedIn} />

                    <div className="container mt-5">
                        <Switch>
                            {protectedRoutes.map(route => (
                                <ProtectedRouteHoc
                                    key={route.path}
                                    isLoggedIn={isLoggedIn}
                                    path={route.path}
                                    component={route.main}
                                    exact={route.exact}
                                    public={route.public}
                                />
                            ))}
                            {routes.map(route => (
                                <Route
                                    key={route.path}
                                    path={route.path}
                                    exact={route.exact}
                                    component={route.main}
                                />
                            ))}
                        </Switch>
                    </div>
                </Router>
            </div>
        </AuthContext.Provider>
    )
}

export default App
