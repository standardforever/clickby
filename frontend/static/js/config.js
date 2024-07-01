const prod_config = {
    name: "production",
    url: "http://app.clickbuy.ai",
    api_url: "http://app.clickbuy.ai/prod-api/api/v1",
    login_redirect: "/login"
}

const test_config = {
    name: "test",
    url: "http://app.clickbuy.ai/test",
    api_url: "http://app.clickbuy.ai/test-api/api/v1",
    login_redirect: "/test/login"
}


const local_config = {
    name: "localhost",
    url: "http://localhost:8003",
    api_url: "http://app.clickbuy.ai/test-api/api/v1",
    login_redirect: "/test/login"
}

export const get_environment_url = () => {
    const path = window.location.pathname;
    const url_variable = window.location.origin;
    
    console.log("path", path)

    let environment;
    if (path.startsWith('/test')) {
        return test_config
    } else if (url_variable === prod_config.url) {
        return prod_config
    } else {
        return local_config
    }
}
