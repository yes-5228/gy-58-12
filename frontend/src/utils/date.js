export function todayISO() {
  return new Date().toISOString().slice(0, 10)
}

export function addDaysISO(offset) {
  const date = new Date()
  date.setDate(date.getDate() + offset)
  return date.toISOString().slice(0, 10)
}
