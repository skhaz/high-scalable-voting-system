import express from 'express'
import http from 'http'
import bodyParser from 'body-parser'
import { createClient } from 'redis'
import client, { Channel, Connection } from 'amqplib'

import { AMQP_DSN, PORT, REDIS_DSN } from './environment'
import { QUEUE } from './constants'

const main = async () => {
  const app = express()

  const server = http.createServer(app)

  const redis = createClient({ url: REDIS_DSN })

  await redis.connect()

  const connection: Connection = await client.connect(AMQP_DSN)

  const channel: Channel = await connection.createChannel()

  await channel.assertQueue(QUEUE)

  app.use(bodyParser.json())

  app.post('/vote', async (req, res) => {
    const { uid } = req.body

    channel.sendToQueue(QUEUE, Buffer.from(uid))

    res.json({ ok: true })
  })

  app.get('/stats/:uid', async (req, res) => {
    const { uid } = req.params

    const counter = await redis.get(uid)

    res.json({ counter })
  })

  app.post('/reset', async (req, res) => {
    await redis.flushDb()

    res.status(204).send()
  })

  server.listen(PORT, async () => {
    console.log(`app listening on port ${PORT}`)
  })
}

main().catch((error) => {
  console.error(error)
})
