if (!process.env.AMQP_DSN) {
  throw new Error('AMQP_DSN environment variable is not defined.')
}

export const { AMQP_DSN } = process.env

if (!process.env.PORT) {
  throw new Error('PORT environment variable is not defined.')
}

export const { PORT } = process.env

if (!process.env.REDIS_DSN) {
  throw new Error('REDIS_DSN environment variable is not defined.')
}

export const { REDIS_DSN } = process.env
