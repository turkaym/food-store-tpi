export function FieldError({ errors }: { errors: unknown[] }) { return errors.length ? <p className="text-sm text-red-600">{errors.join(', ')}</p> : null }
