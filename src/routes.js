import React from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";

const routes = [
  { name: "Join", path: "/", exact: true, main: () => <Login /> },
  { name: "Register", path: "/register", exact: true, main: () => <Register /> }
];

export default routes;
