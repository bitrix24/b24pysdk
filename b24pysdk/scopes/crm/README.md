# Available methods

## crm.activity.type
- crm.activity.type.add
- crm.activity.type.delete
- crm.activity.type.list

## crm.item
- crm.item.fields
- crm.item.add
- crm.item.get
- crm.item.list
- crm.item.update
- crm.item.delete
- crm.item.batch_import

### crm.item.delivery
- crm.item.delivery.get
- crm.item.delivery.list

### crm.item.payment
- crm.item.payment.add
- crm.item.payment.get
- crm.item.payment.list
- crm.item.payment.update
- crm.item.payment.delete
- crm.item.payment.pay
- crm.item.payment.unpay

#### crm.item.payment.delivery
- crm.item.payment.delivery.add
- crm.item.payment.delivery.list
- crm.item.payment.delivery.delete
- crm.item.payment.delivery.set_delivery

#### crm.item.payment.product
- crm.item.payment.product.add
- crm.item.payment.product.list
- crm.item.payment.product.delete
- crm.item.payment.product.set_quantity

### crm.item.productrow
- crm.item.productrow.fields
- crm.item.productrow.add
- crm.item.productrow.get
- crm.item.productrow.list
- crm.item.productrow.update
- crm.item.productrow.delete
- crm.item.productrow.set
- crm.item.productrow.get_available_for_payment

#### crm.item.details.configuration
- crm.item.details.configuration.get
- crm.item.details.configuration.set
- crm.item.details.configuration.reset
- crm.item.details.configuration.force_common_scope_for_all

## crm.orderentity
- crm.orderentity.add
- crm.orderentity.list
- crm.orderentity.delete_by_filter
- crm.orderentity.get_fields

## crm.deal
- crm.deal.fields
- crm.deal.add
- crm.deal.get
- crm.deal.list
- crm.deal.update
- crm.deal.delete

### crm.deal.productrows
- crm.deal.productrows.get
- crm.deal.productrows.set

### crm.deal.contact
- crm.deal.contact.fields
- crm.deal.contact.add
- crm.deal.contact.delete
- crm.deal.contact.items.get
- crm.deal.contact.items.set
- crm.deal.contact.items.delete

#### crm.deal.details.configuration
- crm.deal.details.configuration.get
- crm.deal.details.configuration.set
- crm.deal.details.configuration.reset
- crm.deal.details.configuration.force_common_scope_for_all

### crm.deal.recurring
- crm.deal.recurring.fields
- crm.deal.recurring.add
- crm.deal.recurring.get
- crm.deal.recurring.list
- crm.deal.recurring.update
- crm.deal.recurring.delete
- crm.deal.recurring.expose

### crm.deal.userfield
- crm.deal.userfield.add
- crm.deal.userfield.update
- crm.deal.userfield.get
- crm.deal.userfield.list
- crm.deal.userfield.delete

## crm.lead
- crm.lead.fields
- crm.lead.add
- crm.lead.get
- crm.lead.list
- crm.lead.update
- crm.lead.delete

### crm.lead.productrows
- crm.lead.productrows.get
- crm.lead.productrows.set

### crm.lead.contact
- crm.lead.contact.fields
- crm.lead.contact.add
- crm.lead.contact.delete
- crm.lead.contact.items.get
- crm.lead.contact.items.set
- crm.lead.contact.items.delete

#### crm.lead.details.configuration
- crm.lead.details.configuration.get
- crm.lead.details.configuration.set
- crm.lead.details.configuration.reset
- crm.lead.details.configuration.force_common_scope_for_all

### crm.lead.userfield
- crm.lead.userfield.add
- crm.lead.userfield.update
- crm.lead.userfield.get
- crm.lead.userfield.list
- crm.lead.userfield.delete

## crm.company
- crm.company.fields
- crm.company.add
- crm.company.get
- crm.company.list
- crm.company.update
- crm.company.delete

### crm.company.contact
- crm.company.contact.fields
- crm.company.contact.add
- crm.company.contact.delete
- crm.company.contact.items.get
- crm.company.contact.items.set
- crm.company.contact.items.delete

### crm.company.userfield
- crm.company.userfield.add
- crm.company.userfield.update
- crm.company.userfield.get
- crm.company.userfield.list
- crm.company.userfield.delete

#### crm.company.details.configuration
- crm.company.details.configuration.get
- crm.company.details.configuration.set
- crm.company.details.configuration.reset
- crm.company.details.configuration.force_common_scope_for_all

## crm.contact
- crm.contact.fields
- crm.contact.add
- crm.contact.get
- crm.contact.list
- crm.contact.update
- crm.contact.delete

### crm.contact.company
- crm.contact.company.fields
- crm.contact.company.add
- crm.contact.company.delete
- crm.contact.company.items.get
- crm.contact.company.items.set
- crm.contact.company.items.delete

### crm.contact.userfield
- crm.contact.userfield.add
- crm.contact.userfield.update
- crm.contact.userfield.get
- crm.contact.userfield.list
- crm.contact.userfield.delete

#### crm.contact.details.configuration
- crm.contact.details.configuration.get
- crm.contact.details.configuration.set
- crm.contact.details.configuration.reset
- crm.contact.details.configuration.force_common_scope_for_all

## crm.quote
- crm.quote.fields
- crm.quote.add
- crm.quote.get
- crm.quote.list
- crm.quote.update
- crm.quote.delete

### crm.quote.productrows
- crm.quote.productrows.get
- crm.quote.productrows.set

## crm.requisite
- crm.requisite.fields
- crm.requisite.add
- crm.requisite.get
- crm.requisite.list
- crm.requisite.update
- crm.requisite.delete

### crm.requisite.preset
- crm.requisite.preset.fields
- crm.requisite.preset.add
- crm.requisite.preset.get
- crm.requisite.preset.list
- crm.requisite.preset.update
- crm.requisite.preset.delete
- crm.requisite.preset.countries

#### crm.requisite.preset.field
- crm.requisite.preset.field.fields
- crm.requisite.preset.field.add
- crm.requisite.preset.field.get
- crm.requisite.preset.field.list
- crm.requisite.preset.field.update
- crm.requisite.preset.field.delete
- crm.requisite.preset.field.availabletoadd

### crm.requisite.bankdetail
- crm.requisite.bankdetail.fields
- crm.requisite.bankdetail.add
- crm.requisite.bankdetail.get
- crm.requisite.bankdetail.list
- crm.requisite.bankdetail.update
- crm.requisite.bankdetail.delete

### crm.requisite.userfield
- crm.requisite.userfield.add
- crm.requisite.userfield.update
- crm.requisite.userfield.get
- crm.requisite.userfield.list
- crm.requisite.userfield.delete

### crm.requisite.link
- crm.requisite.link.register
- crm.requisite.link.get
- crm.requisite.link.list
- crm.requisite.link.unregister
- crm.requisite.link.fields

## crm.address
- crm.address.fields
- crm.address.add
- crm.address.list
- crm.address.update
- crm.address.delete

## crm.status
- crm.status.add
- crm.status.delete
- crm.status.fields
- crm.status.get
- crm.status.list
- crm.status.update

### crm.status.entity
- crm.status.entity.items
- crm.status.entity.types

### crm.timeline.bindings
- crm.timeline.bindings.fields
- crm.timeline.bindings.list
- crm.timeline.bindings.bind
- crm.timeline.bindings.unbind

### crm.timeline.comment
- crm.timeline.comment.fields
- crm.timeline.comment.add
- crm.timeline.comment.get
- crm.timeline.comment.list
- crm.timeline.comment.update
- crm.timeline.comment.delete

### crm.timeline.note
- crm.timeline.note.get
- crm.timeline.note.delete
- crm.timeline.note.save

### crm.timeline.logmessage
- crm.timeline.logmessage.add
- crm.timeline.logmessage.get
- crm.timeline.logmessage.list
- crm.timeline.logmessage.delete

### crm.timeline.icon
- crm.timeline.icon.add
- crm.timeline.icon.get
- crm.timeline.icon.list
- crm.timeline.icon.delete

### crm.timeline.logo
- crm.timeline.logo.add
- crm.timeline.logo.get
- crm.timeline.logo.list
- crm.timeline.logo.delete

## crm.userfield
- crm.userfield.fields
- crm.userfield.types

### crm.userfield.enumeration
- crm.userfield.enumeration.fields

### crm.userfield.settings
- crm.userfield.settings.fields