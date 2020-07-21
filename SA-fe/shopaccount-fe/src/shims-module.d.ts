declare module '*.svg' {
    const url: string;
    export default url;
}

declare module '*.jpg' {
const url: string;
export default url;
}

declare module '*.png' {
const url: string;
export default url;
}

declare module '*.json' {
const content: object;
export default content;
}

declare module 'v-charts'{
    const a: any;
    export = a;
}