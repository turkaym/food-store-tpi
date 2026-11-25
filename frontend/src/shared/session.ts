type SessionFailureHandler = () => void

let sessionFailureHandler: SessionFailureHandler | undefined

export function registerSessionFailureHandler(handler: SessionFailureHandler) {
  sessionFailureHandler = handler
}

export function clearClientSession() {
  sessionFailureHandler?.()
}
