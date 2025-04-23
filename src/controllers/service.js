import axios from "axios"

const userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36",
]

const getRandomUserAgent = () => {
    return userAgents[Math.floor(Math.random() * userAgents.length)]
}

const headers = {
    "User-Agent": getRandomUserAgent(),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
    "Referer": "https://bacakomik.one/",
    "Origin": "https://bacakomik.one",
    "X-Requested-With": "XMLHttpRequest",  
    "Upgrade-Insecure-Requests": "1",  
}

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export const fetchPage = async (url, config = {}) => {
    try {
        const response = await axios.get(url, {
            headers: {
                "User-Agent": getRandomUserAgent(),
                ...headers,
                ...config.headers,
            },
            ...config,
        })
        await delay(1000)
        return response.data
    } catch (error) {
        console.error(`Error fetching URL: ${url}`, error.message)
        console.error("Error Response Headers:", error.response?.headers)
        throw error
    }
}
