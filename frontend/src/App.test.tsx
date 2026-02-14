import { render, screen } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'
import { describe, it, expect } from 'vitest'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
})

const renderWithClient = (ui: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  )
}

describe('App', () => {
  it('renders the header and protection card', () => {
    renderWithClient(<App />)
    expect(screen.getAllByText(/ArtShield/i).length).toBeGreaterThan(0)
    expect(screen.getByText(/Protect Your Work/i)).toBeDefined()
  })

  it('renders the upload area initially', () => {
    renderWithClient(<App />)
    expect(screen.getByText(/Click or drag images to shield/i)).toBeDefined()
  })
})
