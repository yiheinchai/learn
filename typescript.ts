type Join<T, Delimiter extends string = '/'> = T extends []
  ? ''
  : T extends [infer L extends string]
    ? L
    : T extends [infer L extends string, ...infer Tail extends [...string[]]]
      ? CleanPath<`${L}${Delimiter}${Join<Tail>}`>
      : never

type CleanPath<T extends string> = T extends `${infer L}//${infer R}`
  ? CleanPath<`${CleanPath<L>}/${CleanPath<R>}`>
  : T extends `${infer L}//`
    ? `${CleanPath<L>}/`
    : T extends `//${infer L}`
      ? `/${CleanPath<L>}`
      : T

type Split<S, TIncludeTrailingSlash = true> = S extends unknown
  ? string extends S
    ? string[]
    : S extends string
      ? CleanPath<S> extends ''
        ? []
        : TIncludeTrailingSlash extends true
          ? CleanPath<S> extends `${infer T}/`
            ? [...Split<T>, '/']
            : CleanPath<S> extends `/${infer U}`
              ? Split<U>
              : CleanPath<S> extends `${infer T}/${infer U}`
                ? [...Split<T>, ...Split<U>]
                : [S]
          : CleanPath<S> extends `${infer T}/${infer U}`
            ? [...Split<T>, ...Split<U>]
            : S extends string
              ? [S]
              : never
      : never
  : never

type ResolveRelativePath<TFrom, TTo = '.'> = TFrom extends string
  ? TTo extends string
    ? TTo extends '.'
      ? TFrom
      : TTo extends `./`
        ? Join<[TFrom, '/']>
        : TTo extends `./${infer TRest}`
          ? ResolveRelativePath<TFrom, TRest>
          : TTo extends `/${infer TRest}`
            ? TTo
            : Split<TTo> extends ['..', ...infer ToRest]
              ? Split<TFrom> extends [...infer FromRest, infer FromTail]
                ? ToRest extends ['/']
                  ? Join<[...FromRest, '/']>
                  : ResolveRelativePath<Join<FromRest>, Join<ToRest>>
                : never
              : Split<TTo> extends ['.', ...infer ToRest]
                ? ToRest extends ['/']
                  ? Join<[TFrom, '/']>
                  : ResolveRelativePath<TFrom, Join<ToRest>>
                : CleanPath<Join<['/', ...Split<TFrom>, ...Split<TTo>]>>
    : never
  : never



type RelativeToPathAutoComplete<
  AllPaths extends string,
  TFrom extends string,
  TTo extends string,
  SplitPaths extends string[] = Split<AllPaths, false>,
> = TTo extends `..${infer _}`
  ? SplitPaths extends [
      ...Split<ResolveRelativePath<TFrom, TTo>, false>,
      ...infer TToRest,
    ]
    ? `${CleanPath<
        Join<
          [
            ...Split<TTo, false>,
            ...(
              | TToRest
              | (Split<
                  ResolveRelativePath<TFrom, TTo>,
                  false
                >['length'] extends 1
                  ? never
                  : ['../'])
            ),
          ]
        >
      >}`
    : never
  : TTo extends `./${infer RestTTo}`
    ? SplitPaths extends [
        ...Split<TFrom, false>,
        ...Split<RestTTo, false>,
        ...infer RestPath,
      ]
      ? `${TTo}${Join<RestPath>}`
      : never
    :
        | (TFrom extends `/`
            ? never
            : SplitPaths extends [...Split<TFrom, false>, ...infer RestPath]
              ? Join<RestPath> extends { length: 0 }
                ? never
                : './'
              : never)
        | (TFrom extends `/` ? never : '../')
        | AllPaths


type AllPaths = '/home/user/documents' | '/home/user/pictures' | '/home/user/videos' | '/home/user/music' | '/home/user/downloads' | '/home/user/desktop' | '/home/user/.config' | '/home/user/.local' | '/home/user/.cache' | '/home/user/.bashrc' | '/home/user/.profile' | '/home/user/.ssh' | '/home/user/.gitconfig'

type Suggestions = RelativeToPathAutoComplete<AllPaths, '/home/user/documents', '..'>