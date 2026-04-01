export default function CarCardSkeleton() {
  return (
    <div className="mm-card rounded-2xl overflow-hidden">
      <div className="h-48 w-full mm-skeleton" />
      <div className="p-4 flex flex-col gap-3">
        <div className="h-5 w-3/4 mm-skeleton rounded-lg" />
        <div className="h-4 w-2/3 mm-skeleton rounded-lg" />
        <div className="flex items-center justify-between mt-2">
          <div className="h-5 w-24 mm-skeleton rounded-lg" />
          <div className="h-9 w-28 mm-skeleton rounded-xl" />
        </div>
      </div>
    </div>
  )
}
