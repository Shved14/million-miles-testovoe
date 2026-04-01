import CarCard from '@/components/CarCard'
import { fetchCars } from '@/lib/api'

export default async function HomePage() {
  const cars = await fetchCars()

  return (
    <main className="min-h-dvh">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <div className="flex items-end justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold">Cars</h1>
            <p className="text-white/60 text-sm">Latest scraped offers</p>
          </div>
        </div>

        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          {cars.map((car) => (
            <CarCard key={car.id} car={car} />
          ))}
        </div>

        {cars.length === 0 ? (
          <div className="mt-10 text-white/60 text-sm">No cars yet.</div>
        ) : null}
      </div>
    </main>
  )
}
