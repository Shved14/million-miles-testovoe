export type Car = {
  id: number
  brand: string
  model: string
  year: number
  mileage: number
  price: number
  image_url: string | null
  created_at: string
}

export function getApiBaseUrl(): string {
  return (
    process.env.API_BASE_URL ||
    process.env.NEXT_PUBLIC_API_BASE_URL ||
    'http://localhost:8000'
  )
}

export async function fetchCars(): Promise<Car[]> {
  const base = getApiBaseUrl()
  const res = await fetch(`${base}/cars`, {
    cache: 'no-store'
  })

  if (!res.ok) {
    throw new Error(`Failed to fetch cars: ${res.status}`)
  }

  return (await res.json()) as Car[]
}
