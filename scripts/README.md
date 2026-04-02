Start with correctly-numbered screens in `sources/caps`

## Crop images

```
python tools/cropper.py
```

> adjust position params - left and width are less critical, we'll trim those later

## Generate bitmaps

```
python tools/bitmapper.py
```

## Slim bitmaps

```
python tools/slimmer.py
```

## Encode bitmaps

```
python tools/rle.py
```
