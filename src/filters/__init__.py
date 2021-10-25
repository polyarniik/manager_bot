from config.loader import dp
from .StaffFilters import IsStaff, IsManager, IsCoordinator

if __name__ == "filters":
    dp.bind_filter(
        IsStaff,
        event_handlers=[
            dp.message_handlers,
            dp.callback_query_handlers,
        ],
    )
    dp.bind_filter(
        IsManager,
        event_handlers=[
            dp.message_handlers,
            dp.callback_query_handlers,
        ],
    )
    dp.bind_filter(
        IsCoordinator,
        event_handlers=[
            dp.message_handlers,
            dp.callback_query_handlers,
        ],
    )
