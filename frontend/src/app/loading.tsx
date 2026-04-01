import CarCardSkeleton from '@/components/CarCardSkeleton'

export default function Loading() {
  return (
    <main className="min-h-dvh">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-8">
          <div className="h-8 w-48 mm-skeleton rounded-xl" />
          <div className="h-4 w-72 mt-3 mm-skeleton rounded-xl" />
        </div>

        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {Array.from({ length: 12 }).map((_, i) => (
            <CarCardSkeleton key={i} />
          ))}
        </div>
      </div>
    </main>
  )
}
