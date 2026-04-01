import Image from 'next/image'

import type { Car } from '@/lib/api'

function formatNumber(value: number): string {
  return new Intl.NumberFormat('en-US').format(value)
}

export default function CarCard({ car }: { car: Car }) {
  const title = `${car.brand} ${car.model}`

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 overflow-hidden">
      <div className="relative h-44 w-full bg-white/5">
        {car.image_url ? (
          <Image
            src={car.image_url}
            alt={title}
            fill
            sizes="(max-width: 768px) 100vw, 33vw"
            className="object-cover"
          />
        ) : (
          <div className="h-full w-full flex items-center justify-center text-white/50 text-sm">
            No image
          </div>
        )}
      </div>

      <div className="p-4 flex flex-col gap-3">
        <div>
          <div className="text-lg font-semibold leading-tight">{title}</div>
          <div className="text-sm text-white/60">
            {car.year} · {formatNumber(car.mileage)} km
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="text-base font-semibold">${formatNumber(car.price)}</div>
          <button className="rounded-xl bg-white text-black px-3 py-2 text-sm font-medium hover:bg-white/90 transition">
            View
          </button>
        </div>
      </div>
    </div>
  )
}
