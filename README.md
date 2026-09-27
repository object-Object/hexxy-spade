# hexxy-spade

## Attaching USB to WSL

```sh
usbipd list
usbipd bind --busid 4-1
usbid attach --wsl --busid 4-1
```
