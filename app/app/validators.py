from django.core.validators import MaxValueValidator

CLICK_POSITION_PERCENTAGE_VALIDATOR = MaxValueValidator(
    100, message="Click position percentage must be in range of 0 to 100"
)
