import Image from 'next/image'

import type { Car } from '@/lib/api'

function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US').format(value)
}

export default function CarCard({ car }: { car: Car }) {
  const title = `${car.brand} ${car.model}`

  return (
    <div className="mm-card rounded-2xl overflow-hidden transition duration-300 hover:-translate-y-1 hover:border-white/20 hover:bg-white/10">
      <div className="relative h-48 w-full bg-white/5">
        {car.image_url ? (
          <Image
            src={car.image_url}
            alt={title}
            fill
            sizes="(max-width: 768px) 100vw, 33vw"
            className="object-cover transition duration-500 hover:scale-[1.03]"
          />
        ) : (
          <div className="h-full w-full flex items-center justify-center text-white/50 text-sm">
            No image
          </div>
        )}
      </div>

      <div className="p-4 flex flex-col gap-3">
        <div>
          <div className="text-base sm:text-lg font-semibold leading-tight tracking-tight">{title}</div>
          <div className="text-sm text-white/60 mt-1">
            {car.year} · {formatNumber(car.mileage)} km
          </div>
        </div>

        <div className="flex items-center justify-between pt-1">
          <div className="text-base sm:text-lg font-semibold">${formatNumber(car.price)}</div>
          <button className="rounded-xl bg-white text-black px-4 py-2 text-sm font-semibold hover:bg-white/90 active:scale-[0.98] transition">
            Подробнее
          </button>
        </div>
      </div>
    </div>
  )
}
