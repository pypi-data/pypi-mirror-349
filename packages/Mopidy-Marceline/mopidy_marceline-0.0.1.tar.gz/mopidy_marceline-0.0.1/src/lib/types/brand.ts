export type Branded<T, B> = T & { __brand: B };

export const brand = <T, B>(value: T): Branded<T, B> => {
    return value as Branded<T, B>;
};
