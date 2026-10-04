from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from serial import Serial

type ResolvedPatternType = Literal[
    "unresolved", "evaluated", "escaped", "undone", "errored", "invalid"
]


PORT = "/dev/ttyUSB0"
BAUD = 19200

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/resolve")
def post_resolve(signature: str) -> ResolvedPatternType:
    encoded = encode_pattern(signature)
    if encoded is None:
        return "invalid"

    try:
        with Serial(PORT, BAUD, timeout=1) as ser:
            ser.write(encoded)
            response = ser.read(1)
        match response:
            case bytes(1):
                return "evaluated"
            case bytes(2):
                return "invalid"
            case _:
                return "errored"
    except Exception as e:  # noqa
        print(e)
        return "errored"


def encode_pattern(signature: str) -> bytes | None:
    if signature.startswith(("aqaa", "dedd")):
        sign = 1 if signature.startswith("aqaa") else -1
        acc = 0
        for angle in signature[4:]:
            match angle:
                case "a":
                    acc <<= 1
                case "q":
                    acc += 5
                case "w":
                    acc += 1
                case "e":
                    acc += 10
                case "d":
                    acc >>= 1
                case _:
                    return None
        acc = (acc * sign) & 0xFFFF_FFFF
        acc &= ~(0b111 << 29)
        return (acc | (6 << 29)).to_bytes(4)
    elif len(signature) <= 5:
        encoded = encode_chunk(signature, False)
        if encoded is None:
            return None
        return encoded.to_bytes(2)
    elif len(signature) <= 10:
        a = encode_chunk(signature[:5], True)
        b = encode_chunk(signature[5:], False)
        if a is None or b is None:
            return None
        return ((a << 16) | b).to_bytes(4)
    else:
        return None


def encode_chunk(signature: str, cont: bool) -> int | None:
    angles: list[int] = []
    for angle in signature[:5]:
        encoded = encode_angle(angle)
        if encoded is None:
            return None
        angles.append(encoded)
    a, b, c, d, e = angles + ([0] * (5 - len(angles)))
    return (a << 13) | (b << 10) | (c << 7) | (d << 4) | (e << 1) | cont


def encode_angle(angle: str):
    match angle:
        case "a":
            return 1
        case "q":
            return 2
        case "w":
            return 3
        case "e":
            return 4
        case "d":
            return 5
        case _:
            return None
