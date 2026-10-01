const TIME_ZONE = process.env.EDIT_KEY_TZ || 'Asia/Kolkata';

// The current date and time as MMyyHHmm, e.g. 29 Sep 2026 22:30 -> "09262230".
// A one minute window on either side covers clock skew and slow typing.
export const timeKeys = (now = Date.now()) => {
    const format = new Intl.DateTimeFormat('en-GB', {
        timeZone: TIME_ZONE,
        year: '2-digit',
        month: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hourCycle: 'h23'
    });
    return [-60000, 0, 60000].map(offset => {
        const parts = Object.fromEntries(
            format.formatToParts(new Date(now + offset)).map(part => [part.type, part.value])
        );
        return `${parts.month}${parts.year}${parts.hour}${parts.minute}`;
    });
};
