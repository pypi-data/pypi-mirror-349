const durationFormat = new Intl.DurationFormat("en", {
    hoursDisplay: "auto",
    minutes: "numeric",
    minutesDisplay: "always",
    seconds: "2-digit",
    secondsDisplay: "always",
    fractionalDigits: 0,
});

export const formatDuration = (duration: number) =>
    durationFormat.format({
        minutes: Math.floor(duration / 60000),
        milliseconds: duration % 60000,
    });
