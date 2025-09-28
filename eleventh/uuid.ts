
export const uuid4 = (prefix?: string) => {
    const id = crypto.randomUUID();
    return prefix ? `${prefix}-${id}` : id;
}
