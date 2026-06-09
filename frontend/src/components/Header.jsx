import { CalendarCheck, Dumbbell } from 'lucide-react'

export function Header({ stats }) {
  return (
    <header className="app-header">
      <div>
        <div className="eyebrow">
          <Dumbbell size={16} />
          Badminton Booking
        </div>
        <h1>羽毛球场地预约系统</h1>
      </div>
      <div className="stat-strip">
        <div>
          <span>今日可预约</span>
          <strong>{stats.available}</strong>
        </div>
        <div>
          <span>待结算</span>
          <strong>{stats.pending}</strong>
        </div>
        <div>
          <span>已支付</span>
          <strong>{stats.paid}</strong>
        </div>
      </div>
      <CalendarCheck className="header-mark" size={42} />
    </header>
  )
}
