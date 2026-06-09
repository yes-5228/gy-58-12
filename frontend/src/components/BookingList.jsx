import { BadgeCheck, CircleX, WalletCards } from 'lucide-react'

export function BookingList({ bookings, courtsById, onSettle, onCancel }) {
  return (
    <section className="panel">
      <div className="section-title">
        <WalletCards size={18} />
        <h2>预约订单</h2>
      </div>
      <div className="booking-list">
        {bookings.length === 0 ? (
          <div className="empty-state">暂无预约订单</div>
        ) : (
          bookings.map((booking) => (
            <article className="booking-item" key={booking.id}>
              <div>
                <strong>{booking.contact_name}</strong>
                <span>
                  {courtsById[booking.court_id]?.name || '未知场地'} · {booking.member_name}
                </span>
              </div>
              <div className="amount-block">
                <span>原价 ¥{booking.original_amount.toFixed(2)}</span>
                <strong>实付 ¥{booking.payable_amount.toFixed(2)}</strong>
              </div>
              <div className={`status-pill ${booking.status}`}>{booking.status}</div>
              <div className="row-actions">
                <button type="button" onClick={() => onSettle(booking.id)} disabled={booking.status !== 'pending'} title="结算">
                  <BadgeCheck size={16} />
                </button>
                <button type="button" onClick={() => onCancel(booking.id)} disabled={booking.status === 'canceled'} title="取消">
                  <CircleX size={16} />
                </button>
              </div>
            </article>
          ))
        )}
      </div>
    </section>
  )
}
