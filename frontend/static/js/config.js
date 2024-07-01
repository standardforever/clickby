const prod_config = {
    name: "production",
    url: "http://app.clickbuy.ai",
    api_url: "http://app.clickbuy.ai/prod-api/api/v1"
}

const test_config = {
    name: "test",
    url: "http://app.clickbuy.ai/test",
    api_url: "http://app.clickbuy.ai/test-api/api/v1"
}


const local_config = {
    name: "localhost",
    url: "http://localhost:8003",
    api_url: "http://app.clickbuy.ai/test-api/api/v1"
}

export const get_environment_url = () => {
    const url_variable = window.location.origin;

    if (url_variable === prod_config.url) {
        return prod_config
    }
    else if (url_variable === test_config.url) {
        return test_config
    }
    else {
        return local_config
    }
}
