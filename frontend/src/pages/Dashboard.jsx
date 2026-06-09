import { useEffect, useMemo, useState } from 'react'
import { api } from '../api/client.js'
import { BookingForm } from '../components/BookingForm.jsx'
import { BookingList } from '../components/BookingList.jsx'
import { CourtSchedule } from '../components/CourtSchedule.jsx'
import { DateTabs } from '../components/DateTabs.jsx'
import { Header } from '../components/Header.jsx'
import { todayISO } from '../utils/date.js'

export function Dashboard() {
  const [courts, setCourts] = useState([])
  const [members, setMembers] = useState([])
  const [slots, setSlots] = useState([])
  const [bookings, setBookings] = useState([])
  const [selectedDate, setSelectedDate] = useState(todayISO())
  const [selectedSlot, setSelectedSlot] = useState(null)
  const [contactName, setContactName] = useState('')
  const [memberId, setMemberId] = useState('1')
  const [message, setMessage] = useState('')

  async function loadBaseData() {
    const [courtData, memberData, bookingData] = await Promise.all([
      api.getCourts(),
      api.getMembers(),
      api.getBookings(),
    ])
    setCourts(courtData)
    setMembers(memberData)
    setBookings(bookingData)
  }

  async function loadSlots(date) {
    const slotData = await api.getTimeSlots(date)
    setSlots(slotData)
    setSelectedSlot(null)
  }

  useEffect(() => {
    loadBaseData().catch((error) => setMessage(error.message))
  }, [])

  useEffect(() => {
    loadSlots(selectedDate).catch((error) => setMessage(error.message))
  }, [selectedDate])

  const courtsById = useMemo(
    () => Object.fromEntries(courts.map((court) => [court.id, court])),
    [courts],
  )

  const stats = useMemo(
    () => ({
      available: slots.filter((slot) => slot.status === 'available').length,
      pending: bookings.filter((booking) => booking.status === 'pending').length,
      paid: bookings.filter((booking) => booking.status === 'paid').length,
    }),
    [slots, bookings],
  )

  async function refresh() {
    await Promise.all([loadSlots(selectedDate), loadBaseData()])
  }

  async function handleCreateBooking(event) {
    event.preventDefault()
    if (!selectedSlot) return
    try {
      await api.createBooking({
        slot_id: selectedSlot.id,
        member_id: Number(memberId),
        contact_name: contactName.trim(),
      })
      setMessage('预约已提交，订单待结算')
      setContactName('')
      await refresh()
    } catch (error) {
      setMessage(error.message)
    }
  }

  async function handleToggleBlock(slot) {
    const status = slot.status === 'blocked' ? 'available' : 'blocked'
    try {
      await api.updateTimeSlot(slot.id, { status })
      await loadSlots(selectedDate)
    } catch (error) {
      setMessage(error.message)
    }
  }

  async function handleSettle(bookingId) {
    await api.settleBooking(bookingId)
    await refresh()
  }

  async function handleCancel(bookingId) {
    await api.cancelBooking(bookingId)
    await refresh()
  }

  return (
    <main className="app-shell">
      <Header stats={stats} />
      <DateTabs selectedDate={selectedDate} onChange={setSelectedDate} />
      {message && <div className="notice">{message}</div>}
      <div className="main-grid">
        <CourtSchedule
          courts={courts}
          slots={slots}
          selectedSlotId={selectedSlot?.id}
          onSelectSlot={setSelectedSlot}
          onToggleBlock={handleToggleBlock}
        />
        <div className="side-stack">
          <BookingForm
            members={members}
            selectedSlot={selectedSlot}
            contactName={contactName}
            memberId={memberId}
            onContactName={setContactName}
            onMemberId={setMemberId}
            onSubmit={handleCreateBooking}
          />
          <BookingList
            bookings={bookings}
            courtsById={courtsById}
            onSettle={handleSettle}
            onCancel={handleCancel}
          />
        </div>
      </div>
    </main>
  )
}
