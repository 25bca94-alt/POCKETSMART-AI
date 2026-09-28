/* =========================================================
   PocketSmartAI - Main JavaScript
   ========================================================= */

"use strict";


/* =========================================================
   Authentication Helpers
   ========================================================= */

/**
 * Get the saved JWT access token.
 */
function getAccessToken() {
    return localStorage.getItem("access_token");
}


/**
 * Save the JWT access token.
 */
function saveAccessToken(token) {
    if (!token) {
        return;
    }

    localStorage.setItem(
        "access_token",
        token
    );
}


/**
 * Remove the saved JWT token.
 */
function clearAccessToken() {
    localStorage.removeItem(
        "access_token"
    );
}


/**
 * Logout the current user.
 */
function logoutUser(event) {

    if (event) {
        event.preventDefault();
    }

    clearAccessToken();

    window.location.href = "/login";
}


/* =========================================================
   API Helper
   ========================================================= */

/**
 * Send a JSON request to the FastAPI backend.
 *
 * @param {string} url
 * @param {object} options
 * @returns {Promise<object>}
 */
async function apiRequest(
    url,
    options = {}
) {

    const requestOptions = {
        method: options.method || "GET",
        headers: {
            ...(options.headers || {})
        }
    };

    if (
        options.body !== undefined &&
        options.body !== null
    ) {
        requestOptions.body =
            typeof options.body === "string"
                ? options.body
                : JSON.stringify(options.body);

        requestOptions.headers[
            "Content-Type"
        ] = "application/json";
    }

    const token = getAccessToken();

    if (token) {
        requestOptions.headers[
            "Authorization"
        ] = "Bearer " + token;
    }

    const response = await fetch(
        url,
        requestOptions
    );

    let data = {};

    try {
        data = await response.json();
    } catch {
        data = {};
    }

    if (!response.ok) {

        if (response.status === 401) {
            clearAccessToken();
        }

        const errorMessage =
            data.detail ||
            "The request could not be completed.";

        throw new Error(errorMessage);
    }

    return data;
}


/* =========================================================
   HTML Safety
   ========================================================= */

/**
 * Escape text before inserting it into HTML.
 *
 * @param {*} value
 * @returns {string}
 */
function escapeHtml(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/* =========================================================
   Date Formatting
   ========================================================= */

/**
 * Format an ISO date into a readable date.
 *
 * @param {*} value
 * @returns {string}
 */
function formatDate(value) {

    if (!value) {
        return "Unknown date";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return String(value);
    }

    return date.toLocaleString(
        undefined,
        {
            dateStyle: "medium",
            timeStyle: "short"
        }
    );
}


/* =========================================================
   Dashboard Authentication
   ========================================================= */

/**
 * Redirect unauthenticated users to login.
 */
function requireLogin() {

    const token = getAccessToken();

    if (!token) {
        window.location.href = "/login";
        return false;
    }

    return true;
}


/* =========================================================
   Dashboard Planner
   ========================================================= */

/**
 * Submit a planner request.
 *
 * This helper can be used by planner pages if needed.
 */
async function submitPlanner(
    plannerType,
    title,
    inputData
) {

    if (!getAccessToken()) {

        window.location.href =
            "/login";

        return null;
    }

    return apiRequest(
        "/api/planners",
        {
            method: "POST",

            body: {
                planner_type: plannerType,
                title: title,
                input_data: inputData
            }
        }
    );
}


/* =========================================================
   History
   ========================================================= */

/**
 * Load planner history.
 */
async function loadHistory() {

    const historyContainer =
        document.getElementById(
            "historyList"
        );

    if (!historyContainer) {
        return;
    }

    if (!requireLogin()) {
        return;
    }

    historyContainer.innerHTML =
        "<p>Loading your history...</p>";

    try {

        const history =
            await apiRequest(
                "/api/planners/history/all"
            );

        if (
            !Array.isArray(history) ||
            history.length === 0
        ) {

            historyContainer.innerHTML =
                '<div class="empty-history">' +
                "<p>No planner history found.</p>" +
                "</div>";

            return;
        }

        historyContainer.innerHTML =
            history
                .map(function (item) {

                    return `
                        <article class="history-card">
                            <h3>
                                ${escapeHtml(
                                    item.planner_type ||
                                    "Planner"
                                )}
                            </h3>

                            <p>
                                <strong>Request:</strong>
                                ${escapeHtml(
                                    item.request_text ||
                                    ""
                                )}
                            </p>

                            <p>
                                <strong>AI Response:</strong>
                                ${escapeHtml(
                                    item.response_text ||
                                    ""
                                )}
                            </p>

                            <p>
                                <strong>Created:</strong>
                                ${escapeHtml(
                                    formatDate(
                                        item.created_at
                                    )
                                )}
                            </p>
                        </article>
                    `;
                })
                .join("");

    } catch (error) {

        console.error(
            "History loading error:",
            error
        );

        historyContainer.innerHTML =
            '<div class="planner-message error">' +
            escapeHtml(
                error.message ||
                "Unable to load history."
            ) +
            "</div>";
    }
}


/* =========================================================
   Login Form
   ========================================================= */

/**
 * Handle login when a page uses
 * the standard login form.
 */
function initializeLoginForm() {

    const form =
        document.getElementById(
            "loginForm"
        );

    if (!form) {
        return;
    }

    const button =
        document.getElementById(
            "loginButton"
        );

    const message =
        document.getElementById(
            "loginMessage"
        );

    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const emailElement =
                document.getElementById(
                    "email"
                );

            const passwordElement =
                document.getElementById(
                    "password"
                );

            if (
                !emailElement ||
                !passwordElement
            ) {
                return;
            }

            const email =
                emailElement.value
                    .trim()
                    .toLowerCase();

            const password =
                passwordElement.value;

            if (!email || !password) {

                if (message) {
                    message.textContent =
                        "Please enter your email and password.";

                    message.className =
                        "planner-message error";
                }

                return;
            }

            if (button) {
                button.disabled = true;
                button.textContent =
                    "Logging in...";
            }

            try {

                const data =
                    await apiRequest(
                        "/api/auth/login",
                        {
                            method: "POST",

                            body: {
                                email: email,
                                password: password
                            }
                        }
                    );

                if (
                    !data ||
                    !data.access_token
                ) {
                    throw new Error(
                        "Login succeeded, but no access token was returned."
                    );
                }

                saveAccessToken(
                    data.access_token
                );

                if (message) {
                    message.textContent =
                        "Login successful. Redirecting...";

                    message.className =
                        "planner-message success";
                }

                window.setTimeout(
                    function () {
                        window.location.href =
                            "/dashboard";
                    },
                    500
                );

            } catch (error) {

                if (message) {

                    message.textContent =
                        error.message ||
                        "Unable to login.";

                    message.className =
                        "planner-message error";
                }

                if (button) {
                    button.disabled = false;
                    button.textContent =
                        "Login";
                }
            }
        }
    );
}


/* =========================================================
   Registration Form
   ========================================================= */

/**
 * Handle user registration.
 */
function initializeRegisterForm() {

    const form =
        document.getElementById(
            "registerForm"
        );

    if (!form) {
        return;
    }

    const button =
        document.getElementById(
            "registerButton"
        );

    const message =
        document.getElementById(
            "registerMessage"
        );

    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const nameElement =
                document.getElementById(
                    "name"
                );

            const emailElement =
                document.getElementById(
                    "email"
                );

            const passwordElement =
                document.getElementById(
                    "password"
                );

            const confirmPasswordElement =
                document.getElementById(
                    "confirmPassword"
                );

            if (
                !nameElement ||
                !emailElement ||
                !passwordElement ||
                !confirmPasswordElement
            ) {
                return;
            }

            const name =
                nameElement.value.trim();

            const email =
                emailElement.value
                    .trim()
                    .toLowerCase();

            const password =
                passwordElement.value;

            const confirmPassword =
                confirmPasswordElement.value;

            if (name.length < 2) {

                showMessage(
                    message,
                    "Please enter your full name.",
                    "error"
                );

                return;
            }

            if (password.length < 6) {

                showMessage(
                    message,
                    "Password must contain at least 6 characters.",
                    "error"
                );

                return;
            }

            if (
                password !==
                confirmPassword
            ) {

                showMessage(
                    message,
                    "Passwords do not match.",
                    "error"
                );

                return;
            }

            if (button) {
                button.disabled = true;
                button.textContent =
                    "Creating Account...";
            }

            try {

                await apiRequest(
                    "/api/auth/register",
                    {
                        method: "POST",

                        body: {
                            name: name,
                            email: email,
                            password: password
                        }
                    }
                );

                showMessage(
                    message,
                    "Account created successfully. Redirecting to login...",
                    "success"
                );

                form.reset();

                window.setTimeout(
                    function () {
                        window.location.href =
                            "/login";
                    },
                    1000
                );

            } catch (error) {

                showMessage(
                    message,
                    error.message ||
                    "Unable to create your account.",
                    "error"
                );

                if (button) {
                    button.disabled = false;
                    button.textContent =
                        "Create Account";
                }
            }
        }
    );
}


/* =========================================================
   Message Helper
   ========================================================= */

function showMessage(
    element,
    text,
    type
) {

    if (!element) {
        return;
    }

    element.textContent = text;

    element.className =
        "planner-message " +
        (type || "");
}


/* =========================================================
   Navigation State
   ========================================================= */

/**
 * Update navigation links based on login state.
 */
function updateNavigation() {

    const token =
        getAccessToken();

    const loginLinks =
        document.querySelectorAll(
            'a[href="/login"]'
        );

    const registerLinks =
        document.querySelectorAll(
            'a[href="/register"]'
        );

    if (!token) {
        return;
    }

    loginLinks.forEach(
        function (link) {

            const hasLogoutHandler =
                link.getAttribute(
                    "onclick"
                ) ===
                "logoutUser(event)";

            if (!hasLogoutHandler) {

                link.textContent =
                    "Dashboard";

                link.href =
                    "/dashboard";
            }
        }
    );

    registerLinks.forEach(
        function (link) {

            link.textContent =
                "Dashboard";

            link.href =
                "/dashboard";
        }
    );
}


/* =========================================================
   DOM Ready
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        initializeLoginForm();

        initializeRegisterForm();

        updateNavigation();

        loadHistory();
    }
);