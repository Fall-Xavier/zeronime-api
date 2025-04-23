import express from "express"
import cors from "cors"
import router from "./routes/router.js"

const app = express()
const PORT = 3000

app.use(cors())
app.use(express.json())

app.use("/api", router)


export default app
