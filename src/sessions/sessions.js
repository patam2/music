import * as Cookies from "js-cookie";
import React from "react";


const getSessionCookie = () => {
    const sessionCookie = Cookies.get('session');

    if (sessionCookie === undefined) {
        return {};
    }
    else {
        return JSON.parse(atob(sessionCookie))
    }
}

export const SessionContext = React.createContext(getSessionCookie());
export default getSessionCookie