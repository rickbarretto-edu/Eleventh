

export type Card = {
    id: string
    name: string
    position: 'atk' | 'mid' | 'def' | 'gk'
    score: number
}