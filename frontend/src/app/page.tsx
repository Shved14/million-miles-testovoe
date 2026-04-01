import CarCard from '@/components/CarCard'
import { fetchCars } from '@/lib/api'

export default async function HomePage() {
  const cars = await fetchCars()

  return (
    <main className="min-h-dvh">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <header className="mb-10">
          <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-white/70">
            Marketplace
          </div>
          <h1 className="mt-4 text-3xl sm:text-4xl font-bold tracking-tight">
            Find your next car
          </h1>
          <p className="mt-3 text-white/60 text-sm sm:text-base max-w-2xl">
            Fresh offers from the daily scraper. Browse by model, year and mileage.
          </p>
        </header>

        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
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
