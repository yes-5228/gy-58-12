import { addDaysISO } from '../utils/date.js'

export function DateTabs({ selectedDate, onChange }) {
  const dates = Array.from({ length: 7 }, (_, index) => addDaysISO(index))

  return (
    <div className="tabs" aria-label="选择日期">
      {dates.map((date) => (
        <button
          key={date}
          className={date === selectedDate ? 'active' : ''}
          onClick={() => onChange(date)}
          type="button"
        >
          {date.slice(5)}
        </button>
      ))}
    </div>
  )
}
