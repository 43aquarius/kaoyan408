declare module "react-syntax-highlighter/dist/esm/prism-async-light" {
  import type { ComponentType } from "react";
  interface PrismProps {
    language?: string;
    style?: Record<string, unknown>;
    customStyle?: Record<string, unknown>;
    wrapLongLines?: boolean;
    codeTagProps?: Record<string, unknown>;
    useInlineStyles?: boolean;
    [key: string]: unknown;
  }
  const PrismAsyncLight: ComponentType<PrismProps> & {
    registerLanguage: (name: string, lang: unknown) => void;
  };
  export default PrismAsyncLight;
}

declare module "react-syntax-highlighter/dist/esm/languages/prism/c" {
  const c: unknown;
  export default c;
}
declare module "react-syntax-highlighter/dist/esm/languages/prism/cpp" {
  const cpp: unknown;
  export default cpp;
}
declare module "react-syntax-highlighter/dist/esm/languages/prism/java" {
  const java: unknown;
  export default java;
}
declare module "react-syntax-highlighter/dist/esm/languages/prism/python" {
  const python: unknown;
  export default python;
}
declare module "react-syntax-highlighter/dist/esm/languages/prism/javascript" {
  const javascript: unknown;
  export default javascript;
}
declare module "react-syntax-highlighter/dist/esm/styles/prism/one-dark" {
  const oneDark: Record<string, unknown>;
  export default oneDark;
}
declare module "react-syntax-highlighter/dist/esm/styles/prism/one-light" {
  const oneLight: Record<string, unknown>;
  export default oneLight;
}
