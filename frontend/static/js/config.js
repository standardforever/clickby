const prod_config = {
    name: "production",
    url: "http://app.clickbuy.ai/",
    api_url: "http://app.clickbuy.ai/prod-api/api/v1"
}

const test_config = {
    name: "test",
    url: "http://app.clickbuy.ai/test/",
    api_url: "http://app.clickbuy.ai/test-api/api/v1"
}


const local_config = {
    name: "localhost",
    url: "http://localhost/",
    api_url: "http://app.clickbuy.ai/test-api/api/v1"
}

export const get_environment_url = () => {
    const url_variable = window.location.origin;
    if (url_variable === prod_config.url) {
        console.log(url_variable, prod_config.name, prod_config.api_url)

        return prod_config.api_url
    }
    else if (url_variable === test_config.url) {
        console.log(url_variable, test_config.name)
    
        return test_config.api_url
    }
    else {
        console.log(url_variable, local_config.name)
        return local_config.api_url
    }
}
